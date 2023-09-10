package main

import (
	"context"
	"fmt"

	"net/http"

	"golang.org/x/net/html"
)

func getXSRFTokenFromInputTag(tag html.Token) string {
	attrs := tag.Attr

	var name string
	var value string

	for _, attr := range attrs {
		switch attr.Key {
		case "name":
			name = attr.Val
		case "value":
			value = attr.Val
		}
	}
	if name == "myradio_login-__xsrf-token" {
		return value
	}

	return ""
}

func (myr *LoginSession) getXSRFTokenFromMyRadio(ctx context.Context) (string, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, "https://ury.org.uk/myradio", nil)
	if err != nil {
		return "", err
	}

	res, err := myr.client.Do(req)
	if err != nil {
		return "", err
	}

	defer res.Body.Close()

	tkn := html.NewTokenizer(res.Body)

	for {
		next := tkn.Next()

		switch next {
		case html.SelfClosingTagToken:
			tag := tkn.Token()

			if tag.Data == "input" {
				if token := getXSRFTokenFromInputTag(tag); token != "" {
					return token, nil
				}
			}
		case html.ErrorToken:
			return "", fmt.Errorf("xsrf token not found")
		}
	}

}
