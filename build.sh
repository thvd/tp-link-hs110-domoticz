docker buildx create --name mybuilder

docker buildx use mybuilder

docker buildx inspect --bootstrap

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 . --push -t theodoorvandonge/tp-link-hs110-domoticz

docker buildx imagetools inspect theodoorvandonge/tp-link-hs110-domoticz

