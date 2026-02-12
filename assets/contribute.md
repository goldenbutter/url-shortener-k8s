## 1. Contributing & Future Improvements

This project is designed to be simple, modular, and easy to extend.  
If you want to contribute or improve the system in the future, here are some recommended areas:



### 🔧 1. Add New Features
- URL expiration (TTL) using Redis `EXPIRE`
- Click analytics (count redirects per short code)
- Custom short codes (user‑defined aliases)
- QR code generation for each short URL
- Admin dashboard for viewing stored URLs



### 🗄️ 2. Improve Storage Layer
- Add Redis authentication (`REDIS_PASSWORD`)
- Add Redis cluster support
- Add PostgreSQL or MongoDB as optional backends
- Add caching layer for frequently accessed URLs



### 🐳 3. Enhance Docker & Deployment
- Add Docker healthchecks for backend and Redis
- Add Docker Compose profiles (dev / prod)
- Add Kubernetes manifests (Deployments, Services, Ingress)
- Add Horizontal Pod Autoscaler (HPA)
- Add CI/CD pipeline (GitHub Actions)



### 🧪 4. Testing & Quality
- Add unit tests for storage layer
- Add integration tests for API endpoints
- Add load testing (k6 / Locust)
- Add linting (flake8, black, isort)



### 📚 5. Documentation
- Expand API documentation
- Add architecture diagram
- Add sequence diagram for request flow
- Add troubleshooting section



### 🤝 6. How to Contribute
1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Submit a pull request  
5. Describe what you improved and why  

All contributions are welcome — from small fixes to major features.

## 2. Contribution Workflow

If you want to improve this project, please follow the workflow below.  
This helps keep development organized and ensures everyone works on clearly defined tasks.



### 📝 1. Create an Issue
Before starting any work:

1. Go to the **Issues** tab in the repository  
2. Create a new issue describing:
   - What you want to improve or fix  
   - Why it’s useful  
   - Any technical notes or ideas  

This helps avoid duplicate work and lets others discuss the idea.



### 👤 2. Assign the Issue to Yourself
Inside the issue page:

- Click **“Assign yourself”**  
- This signals to others that you are actively working on it  

If you cannot assign yourself (permissions), mention in the issue that you are taking it.



### 🍴 3. Fork the Repository
Click **“Fork”** at the top right of the repo.

This creates your own copy where you can safely:

- Add features  
- Fix bugs  
- Experiment  
- Make changes without affecting the main project  



### 🛠️ 4. Implement Your Changes in Your Fork
Inside your fork:

- Create a new branch  
- Make your changes  
- Test everything locally  
- Follow the project’s coding style and structure  

If your change affects deployment (Docker, Compose, Kubernetes), update the README as well with proper screenshots.



### 🔄 5. Submit a Pull Request (PR)
When your work is ready:

1. Go to your fork  
2. Click **“New Pull Request”**  
3. Select your branch → main repository’s `main` branch  
4. Add a clear description:
   - What you changed  
   - Why you changed it  
   - How to test it  

The maintainers will review your PR and merge it if everything looks good.



### 🤝 6. Collaboration Guidelines
- Keep PRs focused on one issue at a time  
- Write clean, maintainable code  
- Add comments where needed  
- Be respectful and constructive in discussions  
- Feel free to ask questions — collaboration is welcome  

---

Contributions of all sizes are appreciated — from small fixes to major features.