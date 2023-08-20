
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "175.110.70.71",
            port: parseInt(12323)
          },
          bypassList: ["foobar.com"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "14aaaad4c03b1",
            password: "31394e0538"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
