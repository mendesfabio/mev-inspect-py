# mev-inspect-py
> illuminating the dark forest 🌲🔦

**mev-inspect-py** is an MEV inspector for Ethereum

Given a block, mev-inspect finds:
- miner payments (gas + coinbase)
- tokens transfers and profit
- swaps and [arbitrages](https://twitter.com/bertcmiller/status/142763202826305946://twitter.com/bertcmiller/status/1427632028263059462)
- ...and more

Data is stored in Postgres for analysis

## Running locally
mev-inspect-py is built to run on kubernetes locally and in production

### Install dependencies

1. Setup a local kubernetes deployment (we use [kind](https://kind.sigs.k8s.io/docs/user/quick-start))

2. Setup [Tilt](https://docs.tilt.dev/install.html) which manages the local deployment

### Start up

Set an environment variable `RPC_URL` to an RPC for fetching blocks
Example:
```
export RPC_URL="http://111.111.111.111:8546"
```

**Note: mev-inspect-py currently requires and RPC with support for parity traces**

Next, start all servcies with:
```
tilt up
```

Press "space" to see a browser of the services starting up

On first startup, you'll need to apply database migrations. Apply with:
```
kubectl exec deploy/mev-inspect-deployment -- alembic upgrade head
```

## Inspecting

### Inspect a single block

Inspecting block [12914944](https://twitter.com/mevalphaleak/status/1420416437575901185)
```
kubectl exec deploy/mev-inspect-deployment -- poetry run inspect-block 12914944
```

### Inspect many blocks

Inspecting blocks 12914944 to 12914954
```
kubectl exec deploy/mev-inspect-deployment -- poetry run inspect-many-blocks 12914944 12914954
```

### Inspect all incoming blocks

Start a block listener with
```
kubectl exec deploy/mev-inspect-deployment -- /app/listener start
```

By default, it will pick up wherever you left off.
If running for the first time, listener starts at the latest block

See logs for the listener with
```
kubectl exec deploy/mev-inspect-deployment -- tail -f listener.log
```

And stop the listener with
```
kubectl exec deploy/mev-inspect-deployment -- /app/listener stop
```

## Contributing

### Guide

✨ Coming soon

### Pre-commit

We use pre-commit to maintain a consistent style, prevent errors, and ensure test coverage. 

To set up, install dependencies through poetry
```
poetry install
```

Then install pre-commit hooks with
```
poetry run pre-commit install
```

### Tests

Run tests with
```
kubectl exec deploy/mev-inspect-deployment -- poetry run pytest --cov=mev_inspect tests
```

## FAQ

### How do I delete / reset my local postgres data?

Stop the system if running
```
tilt down
```

Then delete with
```
kubectl delete pvc data-postgresql-postgresql-0
```

### I was using the docker-compose setup and want to switch to kube, now what?

Make sure the docker-compose resources are down
```
docker compose down
```

Then go through the steps in the current README for kube setup
