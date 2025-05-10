{
  "builds": [
    {
      "src": "./build_files.sh",
      "use": "@vercel/python",
      "config": { "pythonVersion": "3.12" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "index"
    }
  ]
}