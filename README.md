# Site-Update-Notification

Check whether the content of a site gets modified.

## How to Run the Application

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd Site-Update-Notification
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Setup Pushbullet**:
    - Create a Pushbullet account on their [website](https://www.pushbullet.com/) using a Gmail account (it is recommended not to use your main Gmail account).
    - Install the Pushbullet Android app and log in with the same Gmail account. (Despite what their instructions say, you do not need to give any permissions to the Android app, not even notifications.)
    - From the website, go to `Settings -> Account -> Create Access Token`. Copy this token to use in your Python script.

4. **Setup the [.env](http://_vscodecontentref_/0) file**:
    - Create a [.env](http://_vscodecontentref_/1) file in the root directory of the project.
    - Add the Pushbullet API key in the format [key=value](http://_vscodecontentref_/2) pair as shown below:
        ```env
        PUSHBULLET_API_KEY="your_pushbullet_access_token"
        ```

5. **Run the script**:
    ```sh
    python notificare.py --url <URL_TO_SCRAPE> --header_update <HEADER_IN_CASE_OF_SITE_UPDATE> --message_update <MESSAGE_IN_CASE_OF_SITE_UPDATE> --info_header <INFO_HEADER> --info_message <INFO_MESSAGE> --check_interval <CHECK_INTERVAL>
    ```

    - Replace `<URL_TO_SCRAPE>`, `<HEADER_IN_CASE_OF_SITE_UPDATE>`, `<MESSAGE_IN_CASE_OF_SITE_UPDATE>`, `<INFO_HEADER>`, `<INFO_MESSAGE>`, and `<CHECK_INTERVAL>` with your desired values.

## Example

```sh
python notificare.py --url "https://www.example.com" --header_update "Site Updated" --message_update "The site has been updated. Please check." --info_header "Info" --info_message "The program is working fine" --check_interval 60