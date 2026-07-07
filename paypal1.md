I would like to create a checkout template that links from the cart template to check out the items stored within the cart. Within the checkout template the user will need to specify all the details in the `Order(model.Model)` model through a form for delivery details. Use bootstrap formatting including rows, cols and cards. The `Order(model.Model) `model is set up handle multiple different products at the same time, check it to be sure. I wish to use the PayPal Developer Sandbox for payment processing using the PayPal JavaScript SDK v6. The order status already defaults to 'pending' via the Order model, when the payment is accepted it needs to be updated to 'confirmed'.

It MUST use the PayPal JavaScript SDK v6 as paypalrestsdk is depreciated.

As this your model was made before PayPal's v6 SDK I am attaching below in Markdown. 

```markdown
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.paypal.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up JavaScript SDK v6

The PayPal JavaScript SDK v6 enables you to accept the following payment methods on your website:

* PayPal and Pay Later
* Venmo (US only)
* Google Pay
* Apple Pay
* Fastlane guest checkout
* Credit and debit cards

The v6 SDK is faster and more secure than previous versions. It also supports standalone button integrations and iframe-based integrations for stricter security.

<Tip>[Check out a sample integration in GitHub](https://github.com/paypal-examples/v6-web-sdk-sample-integration).</Tip>

## Prerequisites

Before you start, make sure to [get your PayPal client ID and secret](/developer/how-to/api/get-started#1-get-your-client-id-and-client-secret).

If you're a **partner integrating on behalf of other merchants**, follow these additional steps to set up your integration:

* [Onboard as a partner with PayPal](https://developer.paypal.com/docs/multiparty/get-started/)
* [Configure your accounts](https://developer.paypal.com/docs/multiparty/create-account/)
* [Onboard sellers](https://developer.paypal.com/docs/multiparty/seller-onboarding/)
* [Integrate backend with the Orders v2 API](https://developer.paypal.com/docs/multiparty/checkout/advanced/integrate/#integrate-back-end)

## Include the SDK script

Include the v6 SDK script on each page of your site that needs to accept payments.
html theme={null}
<script src="https://www.paypal.com/web-sdk/v6/core"></script>
```
```


For sandbox and testing environments:

```
<script src="https://www.sandbox.paypal.com/web-sdk/v6/core"></script>
```


## Authenticate the SDK

Authenticate with a client ID or a client token. Most integrations should authenticate with a client ID.

<Accordion title="Option A: client ID (recommended)">
  ### Option A: client ID (recommended)

  For most integrations, use your PayPal client ID to authenticate the SDK. You can think of the client ID as your application's user name. This static client ID value is safe to include in your front-end code.

  When to use client ID:

  * Standard checkout integrations (PayPal, cards, Venmo, digital wallets)
  * One-time payments
  * Card vaulting (save card payment methods)
  * Most payment integrations (this is the default)

  <Note>
    Select the tab that matches your integration type:

    * **Direct merchants** process payments into their own PayPal account.
    * **Partners** process payments on behalf of other merchants.
  </Note>

  <Tabs>
    <Tab title="Direct merchants">
      Replace `"YOUR_CLIENT_ID"` with your client ID.

```
const sdkInstance = await window.paypal.createInstance({
        clientId: "YOUR_CLIENT_ID",
        components: ["paypal-payments"],
      });
```

    </Tab>

    <Tab title="Partners">
      * Replace `"YOUR_PARTNER_CLIENT_ID"` with your client ID.
      * Replace `"SELLER_MERCHANT_ID"` with the merchant ID of the seller you're creating the payment session for.

```
const sdkInstance = await window.paypal.createInstance({
        clientId: "YOUR_PARTNER_CLIENT_ID",
        merchantId: "SELLER_MERCHANT_ID",
        components: ["paypal-payments"],
      });
```

    </Tab>
  </Tabs>
</Accordion>

<Accordion title="Option B: client token (for Fastlane only)">
  ### Option B: client token

  <Warning>Client token authentication is required for Fastlane integrations. For all other use cases, use **Option A: client ID**.</Warning>

  A client token is a secure, browser-safe access token generated server-side from your PayPal client ID and secret. This call returns an `access_token` which you use as the client token when you initialize the v6 SDK. Use `expires_in` for caching management on the server side.

  <Note>
    Partner calls must include [`PayPal-Auth-Assertion`](/developer/how-to/api/make-api-requests#paypal-auth-assertion) and [`PayPal-Partner-Attribution-Id`](/developer/how-to/api/make-api-requests#paypal-partner-attribution-id) headers.
  </Note>

  <Info>**Endpoint:** `/v1/oauth2/token/`</Info>

```
curl -X POST 'https://api-m.sandbox.paypal.com/v1/oauth2/token' \
  -u 'PAYPAL_CLIENT_ID:PAYPAL_CLIENT_SECRET' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'domains[]=YOUR_URL1_FOR_THE_SESSION,YOUR_URL2_FOR_THE_SESSION' \
  -d 'response_type=client_token'
```


  <Accordion title="Sample 200 response">
```
{
       "access_token" : "A21AAJrhF-LjFoXzGPJlszGfKg4omnKy5e_eeRXPYzHLb3OdbjtCB3w89nm_6wCCbqn7qSdzjW77VGE7NAJAbXw53ZVpiX5tQ",
       "app_id" : "APP-80W284485P519543T",
       "expires_in" : 32400,
       "nonce" : "2025-10-22T14:32:24ZNpKbSPKuOEA75fCkaNqAcQC_7GbyY1wYSpE1qTeMDaQ",
       "scope" : "https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/payments/futurepayments https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/payments/client-payments-eligibility https://uri.paypal.com/services/identity/activities https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/services/reporting/search/read https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/payments/refund https://uri.paypal.com/services/applications/webhooks https://uri.paypal.com/services/credit/client-offer-presentment/read https://uri.paypal.com/services/paypalhere https://uri.paypal.com/services/disputes/update-seller openid https://uri.paypal.com/services/payments/payment/authcapture Braintree:Vault https://uri.paypal.com/services/disputes/read-seller https://uri.paypal.com/services/payments/orders/client_sdk_orders_api https://uri.paypal.com/services/payments/refund https://uri.paypal.com/payments/payouts https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/shipping/trackers/readwrite https://uri.paypal.com/services/subscriptions https://api.paypal.com/v1/payments/sale/.*/refund",
       "token_type" : "Bearer"
    }
```

  </Accordion>

  The following server-side endpoint returns the client token to your client application. Call this endpoint from your frontend:

```
async function getBrowserSafeClientToken() {
    const response = await fetch("/paypal-api/auth/browser-safe-client-token", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const { accessToken } = await response.json();
    return accessToken;
  }
```

</Accordion>

## Initialize the v6 SDK

Use `window.paypal.createInstance()` to initialize the SDK with your client ID or a client token for authentication. Also, use it to define the components you want to load and to manage other configurations like `locale` and `pageType`. The method returns an SDK instance that provides access to payment eligibility checking and session creation methods.

### `window.paypal.createInstance(options)`

Use `window.paypal.createInstance` to initialize the PayPal SDK. This method configures the SDK for your specific integration needs and returns an SDK instance that you'll use to create payment sessions.

#### Parameters

<table>
  <thead>
    <tr>
      <th align="left">Parameter</th>
      <th align="left">Required</th>
      <th align="left">Description</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td><code>clientId</code></td>
      <td>conditional</td>

      <td>
        <p><strong>string.</strong> Your PayPal client ID. Use this for most integrations. Mutually exclusive with <code>clientToken</code>.</p>
      </td>
    </tr>

    <tr>
      <td><code>clientToken</code></td>
      <td>conditional</td>

      <td>
        <p><strong>string.</strong> A secure, browser-safe token that your server generates using your PayPal client ID and secret. Required for PayPal payment vaulting and Fastlane integrations. This token expires after 15 minutes and is bound to your domain for security. You must generate a new token when needed. Mutually exclusive with <code>clientId</code>.</p>
      </td>
    </tr>

    <tr>
      <td><code>components</code></td>
      <td>no</td>

      <td>
        <p><strong>string\[].</strong> An array of SDK components to load for your integration. Each component enables specific payment functionality.</p>
        <p>Available components:</p>

        <ul>
          <li><code>paypal-payments</code> — PayPal and Pay Later checkout</li>
          <li><code>venmo-payments</code> — Venmo payments (US only)</li>
          <li><code>paypal-guest-payments</code> — Standalone credit or debit card button</li>
          <li><code>paypal-messages</code> — Promotional messaging</li>
          <li><code>card-fields</code> — Inline credit and debit card fields</li>
          <li><code>fastlane</code> — Accelerated guest checkout</li>
          <li><code>googlepay-payments</code> — Google Pay integration</li>
          <li><code>applepay-payments</code> — Apple Pay integration</li>
        </ul>

        <p>Default: <code>\["paypal-payments"]</code></p>
      </td>
    </tr>

    <tr>
      <td><code>pageType</code></td>
      <td>no</td>

      <td>
        <p><strong>string.</strong> The type of page where the SDK is being initialized. This helps PayPal optimize the payment experience and provide better analytics.</p>
        <p>Accepted values:</p>

        <ul>
          <li><code>checkout</code> — Checkout or payment page</li>
          <li><code>product-details</code> — Individual product page</li>
          <li><code>cart</code> — Shopping cart page</li>
          <li><code>mini-cart</code> — Mini cart or side cart</li>
          <li><code>home</code> — Homepage</li>
        </ul>
      </td>
    </tr>

    <tr>
      <td><code>locale</code></td>
      <td>no</td>

      <td>
        <p><strong>string.</strong> The locale for the UI components, specified as a BCP-47 language tag, for example, `"en-US"`, `"fr-FR"`, `"de-DE"`. If not specified, the SDK automatically detects the buyer's locale from their browser settings.</p>
      </td>
    </tr>

    <tr>
      <td><code>clientMetadataId</code></td>
      <td>no</td>

      <td>
        <p><strong>string.</strong> A unique identifier for tracking and debugging. You can generate this using <code>crypto.randomUUID()</code> or your own ID generation system. This ID helps correlate SDK sessions with your server-side logs.</p>
      </td>
    </tr>

    <tr>
      <td><code>merchantId</code></td>
      <td>yes for partners</td>

      <td>
        <p><strong>string.</strong> A unique identifier for the seller you're processing payments for.</p>
      </td>
    </tr>

    <tr>
      <td><code>partnerAttributionId</code></td>
      <td>no</td>

      <td>
        <p><strong>string.</strong> PayPal issues this <code>BN\_CODE</code> to you during partner onboarding.</p>
      </td>
    </tr>
  </tbody>
</table>

#### Returns

Returns a promise that resolves to an SDK instance object. This instance provides methods for checking payment eligibility and creating payment sessions.

* `findEligibleMethods()` - Check payment method availability
* `createPayPalOneTimePaymentSession()` - Create a payment session
* `createFastlane()` - Initialize accelerated guest checkout (Fastlane)

### Example

<Note>
  Partners must include the `merchantId` parameter when initializing the SDK instance. Direct merchants can omit this parameter.
</Note>

```
// Basic initialization with client ID (recommended for most integrations)
const sdkInstance = await window.paypal.createInstance({
  clientId: "YOUR_CLIENT_ID",
});

// With client token (required for PayPal vaulting and fastlane)
const sdkInstance = await window.paypal.createInstance({
  clientToken: "YOUR_CLIENT_TOKEN",
});

// Full configuration with client ID
const sdkInstance = await window.paypal.createInstance({
  clientId: "YOUR_CLIENT_ID",
  components: ["paypal-payments", "venmo-payments"],
  pageType: "checkout",
  locale: "en-US",
  clientMetadataId: crypto.randomUUID(),
});

// With error handling
try {
  const sdkInstance = await window.paypal.createInstance({
    clientId: "YOUR_CLIENT_ID",
  });
  console.log("PayPal SDK initialized successfully");
} catch (error) {
  console.error("Failed to initialize PayPal SDK:", error);
}
```


## Recommended frontend setup

This is the recommended approach for most implementations. It includes all payment methods with eligibility logic and automatic fallback handling. The following are key components of the integration:

### PayPal SDK instance

* **Purpose**: Main entry point for PayPal functionality
* **Components**: Includes `paypal-payments` component
* **Authentication**: Requires client token from server

### Eligibility check

* **Purpose**: Determines payment methods available to the buyer
* **Factors**: User location, currency, account status, device type
* **Implementation**: Always check before showing payment buttons

### Payment sessions

* **PayPal**: Standard PayPal payments
* **Pay Later**: Financing options with specific product codes
* **PayPal Credit**: Credit-based payments with country-specific configuration

### Web components

* `<paypal-button>`: Standard PayPal payment button
* `<paypal-pay-later-button>`: Pay Later financing button
* `<paypal-credit-button>`: PayPal Credit button

### Example

The following is an example of what an `app.js` file might look like when implementing the recommended setup.

<Note>
  Partners must include the `merchantId` parameter when initializing the SDK instance. Direct merchants can omit this parameter.
</Note>

```
async function onPayPalWebSdkLoaded() {
  try {
    // Create PayPal SDK instance
    const sdkInstance = await window.paypal.createInstance({
      clientId: "YOUR_CLIENT_ID",
      components: ["paypal-payments"],
      pageType: "checkout",
    });

    // Check eligibility for all payment methods
    const paymentMethods = await sdkInstance.findEligibleMethods({
      currencyCode: "USD",
    });

    // Set up PayPal button if eligible
    if (paymentMethods.isEligible("paypal")) {
      configurePayPalButton(sdkInstance);
    }

    // Set up Pay Later button if eligible
    if (paymentMethods.isEligible("paylater")) {
      const payLaterPaymentMethodDetails = paymentMethods.getDetails("paylater");
      setupPayLaterButton(sdkInstance, payLaterPaymentMethodDetails);
    }

    // Set up PayPal Credit button if eligible
    if (paymentMethods.isEligible("credit")) {
      const paypalCreditPaymentMethodDetails = paymentMethods.getDetails("credit");
      setupPayPalCreditButton(sdkInstance, paypalCreditPaymentMethodDetails);
    }
  } catch (error) {
    console.error("SDK initialization error:", error);
  }
}

// Shared payment session options for all payment methods
const paymentSessionOptions = {
  // Called when user approves a payment 
  async onApprove(data) {
    console.log("Payment approved:", data);
    try {
      const orderData = await captureOrder({
        orderId: data.orderId,
      });
      console.log("Payment captured successfully:", orderData);
    } catch (error) {
      console.error("Payment capture failed:", error);
    }
  },
  
  // Called when user cancels a payment
  onCancel(data) {
    console.log("Payment cancelled:", data);
  },
  
  // Called when an error occurs during payment
  onError(error) {
    console.error("Payment error:", error);
  },
};

// Set up standard PayPal button
async function configurePayPalButton(sdkInstance) {
  const paypalPaymentSession = sdkInstance.createPayPalOneTimePaymentSession(
    paymentSessionOptions,
  );

  const paypalButton = document.querySelector("paypal-button");
  paypalButton.removeAttribute("hidden");

  paypalButton.addEventListener("click", async () => {
    try {
      await paypalPaymentSession.start(
        { presentationMode: "auto" }, // Auto-detects best presentation mode
        createOrder(),
      );
    } catch (error) {
      console.error("PayPal payment start error:", error);
    }
  });
}

// Set up Pay Later button
async function setupPayLaterButton(sdkInstance, payLaterPaymentMethodDetails) {
  const payLaterPaymentSession = sdkInstance.createPayLaterOneTimePaymentSession(
    paymentSessionOptions
  );

  const { productCode, countryCode } = payLaterPaymentMethodDetails;
  const payLaterButton = document.querySelector("paypal-pay-later-button");

  // Configure button with Pay Later specific details
  payLaterButton.productCode = productCode;
  payLaterButton.countryCode = countryCode;
  payLaterButton.removeAttribute("hidden");

  payLaterButton.addEventListener("click", async () => {
    try {
      await payLaterPaymentSession.start(
        { presentationMode: "auto" },
        createOrder(),
      );
    } catch (error) {
      console.error("Pay Later payment start error:", error);
    }
  });
}

// Set up PayPal Credit button
async function setupPayPalCreditButton(sdkInstance, paypalCreditPaymentMethodDetails) {
  const paypalCreditPaymentSession = sdkInstance.createPayPalCreditOneTimePaymentSession(
    paymentSessionOptions
  );

  const { countryCode } = paypalCreditPaymentMethodDetails;
  const paypalCreditButton = document.querySelector("paypal-credit-button");

  // Configure button with PayPal Credit specific details
  paypalCreditButton.countryCode = countryCode;
  paypalCreditButton.removeAttribute("hidden");

  paypalCreditButton.addEventListener("click", async () => {
    try {
      await paypalCreditPaymentSession.start(
        { presentationMode: "auto" },
        createOrder(),
      );
    } catch (error) {
      console.error("PayPal Credit payment start error:", error);
    }
  });
}
```


## Return order ID to SDK

The `createOrder()` function must return a promise that resolves to `{ orderId: "YOUR_ORDER_ID" }`. This is a key difference between v6 and previous versions of the SDK.

```
// In v6, this must return an object with the shape: { orderId: "YOUR_ORDER_ID" }
  return fetch("/paypal-api/checkout/orders/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(orderPayload),
  })
    .then(response => response.json())
    .then(data => ({ orderId: data.id })); // <-- Required return value
} // End createOrder
```


## Best practices

The following are best practices for integrating the v6 SDK.

Keep sensitive operations server-side and validate all payment data. Provide clear feedback to users throughout the payment flow.

### Security

* Obtain client tokens from your secure server
* Never expose PayPal client secrets in frontend code
* All payment processing happens through PayPal's secure servers
* Never pass up item total from browser - this can be manipulated
* Validate order details on your server before capture

### User experience

* Always check eligibility before showing payment buttons
* Provide clear loading states during payment processing
* Handle popup blockers gracefully with `{ presentationMode:auto }`
* Show appropriate error messages for different failure scenarios

### Performance

* Initialize the SDK early, but avoid blocking page load
* Cache client tokens appropriately
* Use presentation mode fallback strategies

## See also

* [JavaScript SDK v6 reference](/reference/sdk/js/v6/reference)
* [React SDK v6 reference](/reference/sdk/react)
```
