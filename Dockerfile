FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.11-slim AS production

COPY --from=builder /root/.local /root/.local
COPY app/ /app/app/

RUN useradd --no-create-home --shell /bin/false sentryuser

USER sentryuser

EXPOSE 8000

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
