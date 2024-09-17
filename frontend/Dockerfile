# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the frontend code into the container
COPY . .

# Build the React app
RUN yarn run build

# Expose the port where the React app will run
EXPOSE 3000

# Define the command to start the React app
CMD ["yarn", "start"]
