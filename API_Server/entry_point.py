import app.main as app
if __name__ == "__main__":
  app_flask = app.create_app()
  app_flask.run()