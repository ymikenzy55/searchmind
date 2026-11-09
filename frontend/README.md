# SearchMind Frontend

Modern Next.js frontend for SearchMind AI Assistant.

## Features

- 🎨 Beautiful, responsive UI with Tailwind CSS
- 🌓 Dark/light mode with system preference detection
- 🔐 Secure authentication flow
- 💬 Real-time chat interface
- 📱 Fully responsive design

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update with your backend URL.

## Project Structure

```
frontend/
├── app/                    # Next.js app router
│   ├── page.tsx           # Home/Chat page
│   ├── layout.tsx         # Root layout
│   ├── globals.css        # Global styles
│   └── auth/              # Authentication pages
│       ├── login/         # Login page
│       └── register/      # Registration page
├── components/            # React components
│   ├── Chat.tsx          # Main chat interface
│   ├── ThemeProvider.tsx # Theme management
│   └── LoadingSpinner.tsx
├── context/              # React context
│   └── AuthContext.tsx   # Authentication state
└── public/               # Static assets
```

## Customization

### Change Colors

Edit `tailwind.config.ts`:
```typescript
colors: {
  primary: {
    500: '#yourcolor',
  }
}
```

### Modify Chat UI

Edit `components/Chat.tsx` to customize the chat interface.

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for deployment instructions.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript](https://www.typescriptlang.org/docs)
