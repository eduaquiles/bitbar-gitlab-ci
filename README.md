# ![XBar](https://github.com/matryer/xbar/blob/faf87a6ca09fd88c76ad41dce9277b1a74dbe58d/xbarapp.com/public/img/xbar-32.png) XBar plugin for GitLab CI

Shows currently running pipelines from your GitLab in your bar.

![XBar Example](./gitlab_ci.png)

**Forked from https://github.com/pionl/bitbar-gitlab-ci **

## Install

Copy the plugin to your xBar plugins directory. Edit the file and add your gitlab instances to `INSTANCES`.

```
INSTANCES = [
    {
        # Your private key for accessing gitlab: User -> Settings -> Access tokens -> add personal access token with api scope
        'privateToken': 'token',
        # Gitlab URL
        'url': 'https://gitlab.example.com',
        # Define your server and projects (name: id)
        # To get id go to project -> Settings -> General -> General project settings
        'projects': {
            "React": 3,
        },
    },
]
```

> Ensure that the gitlab url is working (urlopen does not follow redirects) #1

--- 

If you have long builds, change the refresh rate (by changing file name).

