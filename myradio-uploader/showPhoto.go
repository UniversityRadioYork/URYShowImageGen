package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"strconv"
)

// SetShowPhoto will take a context, a showIDKey value, and a path to an image
// and set the show image using the *LoginSession
func (e *LoginSession) SetShowPhoto(ctx context.Context, showID int, path string) (string, error) {
	log.Printf("%v | using myradio to set show photo to %s", showID, path)
	img, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer img.Close()

	contents, err := io.ReadAll(img)
	if err != nil {
		return "", err
	}

	stat, err := img.Stat()
	if err != nil {
		return "", err
	}

	body := new(bytes.Buffer)
	writer := multipart.NewWriter(body)
	defer writer.Close()

	part, err := writer.CreateFormFile("sched_showphoto-image_file", stat.Name())
	if err != nil {
		return "", err
	}
	part.Write(contents)

	if err = writer.WriteField("sched_showphoto-show_id", strconv.Itoa(showID)); err != nil {
		return "", err
	}

	if err = writer.WriteField("sched_showphoto-__xsrf-token", e.xsrfToken); err != nil {
		return "", err
	}

	writer.Close()

	log.Printf("%v | doing the upload request", showID)
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, fmt.Sprintf("https://ury.org.uk/myradio/Scheduler/showPhoto?show_id=%v", showID), body)
	if err != nil {
		return "", err
	}

	req.Header.Set("Content-Type", writer.FormDataContentType())
	req.Header.Set("Content-Length", strconv.Itoa(body.Len()))

	_, err = e.client.Do(req)

	return "", err

}
