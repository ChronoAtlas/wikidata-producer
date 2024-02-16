FROM cr.kruhlmann.dev/debian-bookworm-python-3.11 AS compile-image
COPY --chown=$USERNAME:$USERNAME . .
USER $USERNAME
RUN . "$VENV/bin/activate" \
    && make install

FROM cr.kruhlmann.dev/debian-bookworm-python-3.11
COPY --from=compile-image --chown=$USERNAME:$USERNAME "$VENV" "$VENV"
RUN ln -sf "$VENV/bin/wikidata_producer" /usr/local/bin/wikidata_producer
USER $USERNAME
WORKDIR /home/$USERNAME
ENTRYPOINT ["wikidata_producer"]
