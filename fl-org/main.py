import src.app
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.path)
    application = src.create_app()
    application.run(debug=True, host='0.0.0.0', port=80)
