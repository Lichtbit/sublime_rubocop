# RubocopDaemon

A [Sublime Text](http://www.sublimetext.com/) plugin that runs [RuboCop](https://github.com/bbatsov/rubocop) with an [daemon](https://github.com/fohte/rubocop-daemon) on your Ruby files in the editor. It will mark issues right inside the view.

The plugin supports only ST3.

## Installation

### Prerequisites

Please make sure `rubocop-daemon` is installed:

`gem install rubocop-daemon`

### Recommended

Install RubocopDaemon via [Package Control](http://wbond.net/sublime_packages/package_control).

### Manual

1. Navigate to the Sublime Text Packages folder (You can find the location of the Packages folder [here](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory)).

2. Run the git clone command right inside the packages directory: `git clone https://github.com/Lichtbit/sublime_rubocop_daemon "RubocopDaemon"`

3. Restart Sublime Text.

## Configuration

### Per project configuration

You should open your correct project configuration file and add a section: `settings`:

```
{
    "folders":
    [
        {
            "path": "/home/lichtbit/workspace/ruby-project"
        }
    ],
    "settings":
    {
        "rubocop_daemon":
        {
            // Start Rubocop with option "-a"
            "auto_correct": true,

            // Start Rubocop with option "-A"
            // possible since rubocop 0.87
            // https://github.com/rubocop-hq/rubocop/releases/tag/v0.87.0
            "auto_correct_all": true,

            // Rubocop config file "--config"
            "config_file": "/home/lichtbit/workspace/ruby-project/config/rubocop.yml",

            // Disable RubocopDaemon for this project
            "disabled": false,

            // Start daemon automaticly with command (seperate arguments with array)
            "start_daemon_automaticly": ["/home/lichtbit/.rvm/wrappers/ruby-2.5.3@m3/rubocop-daemon", "start"],

            // Workspace, to use use "cd" before starting rubocop
            "workspace": "/home/lichtbit/workspace/ruby-project/",

            // Mark rubocop issues in view
            "mark_issues_in_view": true
        }
    }
}
```

### Per global configuration

_Preferences > Package Settings > RubocopDaemon > Settings-User_



## What can it do for you?

By default, the plugin marks Rubocop issues right in the view when you open or save a Ruby file.

## Credits

The plugin was forked from [Sublime RuboCop](https://github.com/pderichs/sublime_rubocop). So thanks go out to all [contributors](https://github.com/pderichs/sublime_rubocop/graphs/contributors).

Thanks go out to all [contributors of rubocop](https://github.com/bbatsov/rubocop/graphs/contributors) and [contributors of rubocop-daemon](https://github.com/fohte/rubocop-daemon/graphs/contributors)

## License

All of RubocopDaemon is licensed under the MIT license.

  Copyright (c) 2018 Georg Limbach <georg.limbach@lichtbit.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
