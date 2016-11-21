#Twitter NLP
Twitter NLP is a microservice-based web application for analyzing Twitter sentiment in real time. The goal of the project is to show how to deploy a machine learning model, apply it in real time, and scale the model.

## Architecture

![Alt text](/readme/architecture.png?raw=true "architecture")


## Deploying the app on Pivotal Cloud Foundry

```
cf create-service p-redis shared-vm twitter-nlp-redis
cf push
```


## Notes

The project was inspired in part by [BirdWatch](https://github.com/matthiasn/BirdWatch)

