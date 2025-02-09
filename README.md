# Site-Update-Notification

Check whether the content of a site gets modified.

## Prerequisites

- Python (version 3.6 or higher) should be installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

## How to Run the Application

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd Site-Update-Notification
    ```

2. **Create a virtual environment**:
    - It is recommended to create a virtual environment inside the `Site-Update-Notification` folder:
        ```sh
        python -m venv <virtual_environment_name>
        ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        <virtual_environment_name>\Scripts\activate
        ```

4. **Install the required dependencies**:
    - With the virtual environment activated, install the dependencies:
        ```sh
        <virtual_environment_name>\Scripts\pip install .
        ```

5. **Setup Pushbullet**:
    - Create a Pushbullet account on their [website](https://www.pushbullet.com/) using a Gmail account (it is recommended not to use your main Gmail account).
    - Install the Pushbullet Android app and log in with the same Gmail account. (Despite what their instructions say, you do not need to give any permissions to the Android app, not even notifications.)
    - From the website, go to `Settings -> Account -> Create Access Token`. Copy this token to use in your Python script.

6. **Setup the [.env](http://_vscodecontentref_/0) file**:
    - Rename the [template.env](http://_vscodecontentref_/1) file to [.env](http://_vscodecontentref_/2).
    - Add the Pushbullet API key in the format `key=value` pair as shown below, replacing the placeholder key with your actual Pushbullet API key:
        ```env
        PUSHBULLET_API_KEY="your_pushbullet_access_token"
        ```

7. **Run the script**:
    - Only the URL is a mandatory argument for the script. Other arguments are optional and can be customized as needed.
    ```sh
    python notificare.py --url <URL_TO_SCRAPE> --header_update <HEADER_IN_CASE_OF_SITE_UPDATE> --message_update <MESSAGE_IN_CASE_OF_SITE_UPDATE> --info_header <INFO_HEADER> --info_message <INFO_MESSAGE> --check_interval <CHECK_INTERVAL>
    ```

    - Replace `<URL_TO_SCRAPE>`, `<HEADER_IN_CASE_OF_SITE_UPDATE>`, `<MESSAGE_IN_CASE_OF_SITE_UPDATE>`, `<INFO_HEADER>`, `<INFO_MESSAGE>`, and `<CHECK_INTERVAL>` with your desired values.

## Example

```sh
python notificare.py --url "https://www.example.com" --header_update "Site Updated" --message_update "The site has been updated. Please check." --info_header "Info" --info_message "The program is working fine" --check_interval 60