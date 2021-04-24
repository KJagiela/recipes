FROM python:3.9.2-slim-buster as development-stage

ARG USER_ID
ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # user
  USER_ID=${USER_ID} \
  HOME=/home/django \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # dockerize
  DOCKERIZE_VERSION=v0.6.1 \
  # poetry
  POETRY_VERSION=1.1.5 \
  POETRY_CACHE_DIR=/var/cache/pypoetry

RUN apt-get -qq update \
    && apt-get -qq -y install \
        curl \
        gettext \
        git \
        make \
        openssl \
        tini \
    && apt-get -qq -y autoremove \
    && apt-get -qq -y clean \
    && rm -rf /var/lib/apt/lists/* \
    # Install dockerize
    && curl \
        --location \
        --silent \
        --output "./dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
        "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar \
        -C /usr/local/bin \
        -xzvf "./dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "./dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    # Install poetry
    && pip install --upgrade --force-reinstall pip \
    && pip install "poetry==${POETRY_VERSION}"


COPY ./.devops/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./.devops/docker/start.sh /start.sh
RUN chmod +x /start.sh

# Create the user and group to run the Django application as
RUN addgroup --system --gid ${USER_ID} django \
    && adduser --system --home ${HOME} --uid ${USER_ID} --ingroup django django

WORKDIR /app

# Install python dependencies
COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
# Force `virtualenvs.create false` in case user update it in `pyproject.toml`
RUN poetry config virtualenvs.create false \
  && poetry install \
    $(if [ "${DJANGO_ENV}" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction \
    --no-ansi \
  # Cleaning poetry installation's cache for production:
  && if [ "${DJANGO_ENV}" = 'production' ]; then rm -rf "${POETRY_CACHE_DIR}"; fi


ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD ["/start.sh"]

COPY ./backend /app
#RUN chown -R django /app /home/django
#USER django


FROM development-stage as production-stage

USER root
# Override `/start.sh` to serve app with `gunicorn`
COPY ./.devops/docker/gunicorn.sh /start.sh
RUN chmod +x /start.sh

COPY --chown=django:django ./backend /app
COPY --chown=django:django ./shared/static /app/static
USER django
