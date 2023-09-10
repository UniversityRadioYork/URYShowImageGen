package main

import (
	"context"
	"os"
	"strconv"
)

func main() {
	// usage: ./myradio-uploader myradio-user myradio-pass showid photopath
	// i.e. ./myradio-uploader user1 password1 12345 tmp-img.png

	session, err := CreateMyRadioLoginSession(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}

	ctx, cnl := context.WithTimeout(context.Background(), session.timeout)
	defer cnl()

	showID, err := strconv.Atoi(os.Args[3])
	if err != nil {
		panic(err)
	}

	_, err = session.SetShowPhoto(ctx, showID, os.Args[4])

	if err != nil {
		panic(err)
	}
}
