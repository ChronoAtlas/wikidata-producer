ARG PYTHON_VERSION=3.11

FROM cr.kruhlmann.dev/debian-bookworm-python-${PYTHON_VERSION} AS compile-image
COPY --chown=$USERNAME:$USERNAME . .
USER $USERNAME
RUN . "$VENV/bin/activate" \
    && make install

FROM cr.kruhlmann.dev/debian-bookworm-python-${PYTHON_VERSION}
COPY --from=compile-image --chown=$USERNAME:$USERNAME "$VENV" "$VENV"
RUN ln -sf "$VENV/bin/wikidata_producer" /usr/local/bin/wikidata_producer
USER $USERNAME
WORKDIR /home/$USERNAME
ENTRYPOINT ["wikidata_producer"]
