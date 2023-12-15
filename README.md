<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://t.me/unforgivingbot">
    <img src="logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Unforgivingbot</h1>

  <p align="center">
    Telegram bot to help you remember your bets with friends
    <br />
    <a href="https://t.me/unforgivingbot"><strong>Try out the bot in telegram »</strong></a>
    <br />
    <br />
    <a href="https://github.com/gushcha/unforgivingbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/gushcha/unforgivingbot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This app is a simple bot which will notify you about a bet.

To use it you just need to submit a dispute in any telegram chat via inline mode.

For example:
```
@unforgivingbot I bet, I'll mangage to end development of a telegram bot before 31.12.2044
```

Click on a bot proposal, if it says the bot will remind you on a date you specified.

In response the bot will add message to chat with dispute details and a "Subscribe" button.
By clicking "Subscribe" you will be reminded on dispute end date.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![python][python.org]][python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Bot is written in python and uses dockered postgres dbms, please make sure following is installed on your system:

* python@3.11
* docker
* git

### Installation

1. Create new telegram bot using [botfather](https://t.me/botfather)

2. Clone the repo
   ```sh
   sudo git clone https://github.com/gushcha/unforgivingbot.git
   cd unforgivingbot
   ```

3. Create `config.yml` with same contents as `config.default.yml` and add the bot token received from botfather
  ```sh
   sudo cp config.default.yml config.yml
   sudo vim config.yml
   ```

4. Create python virtual environment and install dependencies
   ```sh
   sudo python3 -m venv venv
   source venv/bin/activate
   python3 -m pip install -r requirements.txt
   sudo mkdir /var/log/unforgiving/
   sudo chown -R $USER /var/log/unforgiving/
   sudo chmod -R g+rw /var/log/unforgiving/
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Bot consists of multiple running services `docker postgres`, `notifier` and `submitter`

1. Create database and start it
    ```sh
    . ./scripts/db_start.sh
    ```

2. Add notifier cron
   ```sh
   sudo bash ./scripts/start_notifier_cron.sh
   ```

3. Start submitter listener
    ```sh
    sudo bash ./scripts/create_submitter_service.sh
    sudo systemctl start unforgivingbot.service
    cd ../
    python3 start_submitter.py 
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Readme
- [ ] Proper error handling
- [ ] Add keyboard calendar entry
- [ ] Timezone support
- [ ] Multi-language Support
    - [ ] Russian
    - [ ] Greek

See the [open issues](https://github.com/gushcha/unforgivingbot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python.org]: https://img.shields.io/badge/python-FFD343?style=for-the-badge&logo=python
[python-url]: https://www.python.org 