# SkyPro cli tool

## How to start

Show current config

```commandline
sky-cli config
```

Reconfigure SkyPro access

```commandline
sky-cli config --skypro
```

If SkyPro credentials are missing, the `summary` command exits with an error.
Configure them first with `sky-cli config --skypro`.

Check money you earned this month

```commandline
sky-cli summary
```

Another month or year

```commandline
sky-cli summary --month 3 --year 2026
```

You can see outcoming lives

```commandline
sky-cli lives
```
