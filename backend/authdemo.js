const express = require('express');

require('dotenv').config();

let router = express.Router();

const { auth, requiresAuth } = require('express-openid-connect');
const { response } = require('express');
const { nextTick } = require('process');
router.use(
  auth(
  {
    authRequired: false,
    auth0Logout: true,
    issuerBaseURL: process.env.ISSUER_BASE_URL,
    baseURL: process.env.BASE_URL,
    clientID: process.env.CLIENT_ID,
    secret: process.env.SECRET,
    idpLogout: true,
    routes: {
      // Override the default login route to use your own login route as shown below
      login: false,
      // Pass a custom path to redirect users to a different
      // path after logout.
      postLogoutRedirect: '/custom-logout',
    },
  })
);

router.get('/login', requiresAuth(), (request, response) => {
  response.redirect(BACKENDHOST+"/welcome.html");
});

router.get('/custom-logout', (request, response) => {
  response.redirect(BACKENDHOST);
});

// req.isAuthenticated is provided from the auth router
router.get('/', (request, response) => {
  response.send(request.oidc.isAuthenticated() ? 'Logged in' : 'Logged out')
});

//router.get('/user', (request, response) => {
//   response.send(JSON.stringify(request.oidc.user));
//});


module.exports = {router} ;

