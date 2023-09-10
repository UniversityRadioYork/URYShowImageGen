package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// LoginSession provides a login session for MyRadio after authenticating
// with a MyRadio username and password
type LoginSession struct {
	client    *http.Client
	xsrfToken string
	timeout   time.Duration
}

// Close will log out the MyRadio session
func (e *LoginSession) Close() {
	log.Printf("logging out of myradio")
	ctx, cnl := context.WithTimeout(context.Background(), e.timeout)
	defer cnl()

	form := url.Values{
		"myradio_logout-__xsrftoken": []string{e.xsrfToken},
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, "https://ury.org.uk/myradio/MyRadio/logout", strings.NewReader(form.Encode()))
	if err != nil {
		return
	}

	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	e.client.Do(req)
}

// CreateMyRadioLoginSession gets an XSRF token from MyRadio, and will
// then log in to MyRadio, returning the LoginSession
func CreateMyRadioLoginSession(username, password string) (*LoginSession, error) {
	log.Printf("creating myradio login session for user %s", username)
	myr := LoginSession{
		client: http.DefaultClient,
	}

	myr.client.Jar = cookieJar{
		cookies: make(map[string][]*http.Cookie),
	}

	myr.timeout = time.Duration(5) * time.Second

	ctx, cnl := context.WithTimeout(context.Background(), time.Duration(2)*myr.timeout)
	defer cnl()

	log.Println("getting myradio xsrf token for this session")
	var err error
	myr.xsrfToken, err = myr.getXSRFTokenFromMyRadio(ctx)
	if err != nil {
		log.Printf("failed to get myradio xsrf token: %v", err)
		return nil, err
	}

	log.Printf("logging in to myradio as %s", username)
	if err := myr.login(ctx, username, password); err != nil {
		log.Printf("failed to login: %v", err)
		return nil, err
	}

	return &myr, nil
}

func (e *LoginSession) login(ctx context.Context, username, password string) error {
	form := url.Values{
		"myradio_login-user":         []string{username},
		"myradio_login-password":     []string{password},
		"myradio_login-next":         []string{"/myradio"},
		"myradio_login-__xsrf-token": []string{e.xsrfToken},
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, "https://ury.org.uk/myradio/MyRadio/login", strings.NewReader(form.Encode()))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	res, err := e.client.Do(req)
	if err != nil {
		return err
	}

	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("not OK: %v", res.Status)
	}

	return nil

}
