# Queuing System in JavaScript

This project implements a simple queuing system using **Node.js**, **Express**, **Redis**, and **Kue** to handle background jobs and cache data. The purpose of this project is to learn and integrate these technologies to build a backend system that processes tasks in the background while managing data efficiently.

## Learning Objectives

By the end of this project, you should be able to:

- Run a Redis server on your machine.
- Perform basic Redis operations using a Node.js Redis client.
- Store hash values in Redis.
- Handle asynchronous operations with Redis.
- Use **Kue** as a queuing system with Redis.
- Build a basic Express app that interacts with a Redis server.
- Build a basic Express app that interacts with both Redis and Kue.

---

## Prerequisites

Before you start, make sure you have the following installed:

- **Node.js**: JavaScript runtime for the server.
- **Redis**: In-memory data store (used for caching and background jobs).
- **npm**: Node.js package manager.

---

## Getting Started

### Step 1: Install Redis

#### macOS
```bash
brew install redis
```

#### Windows
You can use the Windows Subsystem for Linux (WSL) or Docker.

#### Linux (Debian/Ubuntu)
```bash
sudo apt install redis-server
```

To start Redis:
```bash
redis-server
```

Check if Redis is running by using the Redis CLI:
```bash
redis-cli
```

---

### Step 2: Set up the Project

1. **Clone this repository** or create a new directory for your project:
    ```bash
    mkdir queuing-system
    cd queuing-system
    ```

2. **Initialize a new Node.js project**:
    ```bash
    npm init -y
    ```

3. **Install Dependencies**:
    ```bash
    npm install express redis kue
    ```

---

### Step 3: Basic Redis Operations in Node.js

Create a file `index.js` and add the following code to interact with Redis:

```js
const redis = require('redis');
const client = redis.createClient();

client.on('connect', () => {
  console.log('Connected to Redis');
});

// Simple Redis Operations
client.set('name', 'John Doe', redis.print);
client.get('name', (err, reply) => {
  console.log(reply);  // Output: John Doe
});

// Storing hash values
client.hset('user:1000', 'name', 'John', redis.print);
client.hget('user:1000', 'name', (err, reply) => {
  console.log(reply);  // Output: John
});
```

Run the script:
```bash
node index.js
```

---

### Step 4: Asynchronous Operations with Redis

Since Redis operations are asynchronous, here's how to handle them using Promises and `async/await`:

```js
const redis = require('redis');
const util = require('util');

const client = redis.createClient();
client.get = util.promisify(client.get);

async function getUser() {
  const user = await client.get('user:1000');
  console.log(user);
}

getUser();
```

---

### Step 5: Setting Up Kue for Job Queueing

1. **Create a job queue** using Kue:

```js
const kue = require('kue');
const queue = kue.createQueue();

// Create a job
queue.create('email', {
  title: 'Welcome Email',
  to: 'john@example.com',
  from: 'support@example.com',
}).save();

// Process the job
queue.process('email', (job, done) => {
  console.log('Sending email to:', job.data.to);
  done();
});
```

2. To run Kue's UI to monitor jobs, use this URL: `http://localhost:3000`.

---

### Step 6: Building a Basic Express App

Now let's integrate **Express** into the project.

Create an `app.js` file:

```js
const express = require('express');
const app = express();
const redis = require('redis');
const kue = require('kue');

const client = redis.createClient();
const queue = kue.createQueue();

// Define routes
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Route to create a job
app.post('/job', (req, res) => {
  queue.create('email', {
    title: 'Send Email',
    to: 'john@example.com',
  }).save((err) => {
    if (err) return res.status(500).send('Error creating job');
    res.send('Job created');
  });
});

// Process jobs
queue.process('email', (job, done) => {
  console.log('Sending email to:', job.data.to);
  done();
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

Run the app:
```bash
node app.js
```

---

### Step 7: Using Redis for Caching in Express

We can also use Redis to cache data. Here's an example of how to set up caching with Redis in your Express app:

```js
app.get('/cache', (req, res) => {
  const key = 'someData';

  client.get(key, (err, data) => {
    if (data) {
      return res.send(`Cache: ${data}`);
    }

    // Fetch new data if not in cache
    const newData = 'Fetched new data!';
    client.setex(key, 3600, newData);  // Set cache with expiration
    return res.send(`New: ${newData}`);
  });
});
```

---

### Step 8: Combine Redis, Kue, and Express

Finally, let's integrate **Redis**, **Kue**, and **Express** to build a full-fledged backend that handles background jobs and caching:

```js
const express = require('express');
const kue = require('kue');
const redis = require('redis');
const app = express();

const queue = kue.createQueue();
const client = redis.createClient();

// Endpoint to create a job
app.post('/job', (req, res) => {
  queue.create('email', {
    title: 'Send Email',
    to: 'john@example.com',
  }).save((err) => {
    if (err) return res.status(500).send('Error creating job');
    res.send('Job created');
  });
});

// Job processing
queue.process('email', (job, done) => {
  console.log('Sending email to:', job.data.to);
  done();
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## Running the Application

1. Start the Redis server in one terminal:
   ```bash
   redis-server
   ```

2. Run your Express app in another terminal:
   ```bash
   node app.js
   ```

3. You can now access the Express app by visiting `http://localhost:3000` in your browser.

---

## Conclusion

By completing this project, you will have gained experience in:

- Setting up and using **Redis** for caching and as a message broker.
- Using **Kue** to handle background jobs and queues.
- Building an **Express** web application that interacts with Redis and Kue.

These skills are foundational for building scalable, high-performance backend systems.

---

## Resources

- [Redis Documentation](https://redis.io/docs/)
- [Kue Documentation](https://github.com/Automattic/kue)
- [Express Documentation](https://expressjs.com/)
