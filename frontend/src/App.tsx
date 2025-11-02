import { useState, useEffect } from 'react';
import {
  Container,
  CssBaseline,
  ThemeProvider,
  createTheme,
  AppBar,
  Toolbar,
  Typography,
  Box,
} from '@mui/material';
import ImageUpload from './components/ImageUpload';
import Timeline from './components/Timeline';
import { ImagePost } from './types';

// Material Design theme with Apple HIG principles
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#007AFF', // iOS blue
      light: '#5AC8FA',
      dark: '#0051D5',
    },
    secondary: {
      main: '#FF9500', // iOS orange
    },
    background: {
      default: '#F2F2F7', // iOS system background
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    h4: {
      fontWeight: 600,
      letterSpacing: '-0.5px',
    },
  },
  shape: {
    borderRadius: 12, // Apple's rounded corners
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
          transition: 'all 0.3s cubic-bezier(.25,.8,.25,1)',
          '&:hover': {
            boxShadow: '0 4px 6px rgba(0,0,0,0.16), 0 2px 4px rgba(0,0,0,0.23)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 10,
        },
      },
    },
  },
});

function App() {
  const [images, setImages] = useState<ImagePost[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchImages = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/images');
      const data = await response.json();
      setImages(data);
    } catch (error) {
      console.error('Error fetching images:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const handleImageUploaded = () => {
    fetchImages();
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="sticky" elevation={0} sx={{ backdropFilter: 'blur(20px)', backgroundColor: 'rgba(255,255,255,0.8)' }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600, color: 'text.primary' }}>
              Image Timeline
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="md" sx={{ py: 4 }}>
          <ImageUpload onImageUploaded={handleImageUploaded} />
          <Timeline images={images} loading={loading} />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
