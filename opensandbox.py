#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

print(SCRIPT_DIR)

def build_image():
    print("Building opensandbox image...")
    subprocess.run([
        "podman", "build", "-t", "opensandbox", "-f", "Dockerfile.arch", SCRIPT_DIR
    ], check=True)
    print("Image built successfully.")


def image_exists():
    result = subprocess.run(
        ["podman", "image", "inspect", "opensandbox"],
        capture_output=True
    )
    return result.returncode == 0


def create_container(tag, mount):
    if not image_exists():
        print("Image not found, building...")
        build_image()

    print(f"Creating sandbox '{tag}' with mount '{mount}'...")
    subprocess.run([
        "podman", "run", "-it",
        "--runtime", "crun",
        "--annotation", "run.oci.handler=krun",
        "--name", tag,
        "-v", f"{mount}:/workspace",
        "opensandbox",
    ], check=True)
    print(f"Sandbox '{tag}' created and running.")
    print(f"Mounted '{mount}' at /workspace in sandbox.")


def open_container(tag):
    print(f"Starting and attaching to sandbox '{tag}'...")
    subprocess.run([
        "podman", "start", "-ai", tag
    ], check=True)


def list_containers():
    result = subprocess.run([
        "podman", "ps", "-a", "--filter", "ancestor=opensandbox",
        "--format", "{{.Names}} {{.CreatedAt}}"
    ], capture_output=True, text=True)
    print(f"{'NAME':<20} CREATED")
    for line in result.stdout.strip().split("\n"):
        if line:
            parts = line.split(" ", 1)
            name = parts[0]
            created = parts[1][:19] if len(parts) > 1 else ""
            print(f"{name:<20} {created}")


def remove_container(tag):
    print(f"Removing sandbox '{tag}'...")
    subprocess.run(["podman", "rm", "-f", tag], check=True, capture_output=True)
    print(f"Sandbox '{tag}' removed.")


def main():
    parser = argparse.ArgumentParser(prog="sandbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build/rebuild the opensandbox image")

    create_parser = subparsers.add_parser("create", help="Create a new sandbox and run opencode")
    create_parser.add_argument("tag", help="Tag/name for the sandbox")
    create_parser.add_argument("mount", help="Path to mount into /workspace")

    start_parser = subparsers.add_parser("start", help="Attach to an existing sandbox")
    start_parser.add_argument("tag", help="Tag/name of the sandbox to open")

    list_parser = subparsers.add_parser("list", help="List sandboxes from opensandbox image")

    remove_parser = subparsers.add_parser("remove", help="Remove a sandbox by tag")
    remove_parser.add_argument("tag", help="Tag/name of the sandbox to remove")

    args, unknown = parser.parse_known_args()

    if args.command == "build":
        build_image()
    elif args.command == "create":
        create_container(args.tag, args.mount)
    elif args.command == "start":
        open_container(args.tag)
    elif args.command == "list":
        list_containers()
    elif args.command == "remove":
        remove_container(args.tag)


if __name__ == "__main__":
    main()
