from application.application import application


if __name__ == "__main__":
    application.run(host="localhost", port=6002, debug=True)