FROM golang:1.22-alpine AS golang-builder

RUN addgroup -S query && adduser -S query -G query

WORKDIR /src/app
COPY --chown=query:query . .

RUN go get
RUN go build

FROM scratch
COPY --from=golang-builder /src/app/QueryProcessor /QueryProcessor
COPY --from=golang-builder /etc/passwd /etc/passwd

USER query

EXPOSE 8080

CMD [ "/QueryProcessor" ]
