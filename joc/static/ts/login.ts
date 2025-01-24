const sessionCookieInput = document.getElementById('session_cookie') as HTMLInputElement;
sessionCookieInput.value = document.cookie.replace(/(?:(?:^|.*;\s*)sessionid\s*\=\s*([^;]*).*$)|^.*$/, "$1");
