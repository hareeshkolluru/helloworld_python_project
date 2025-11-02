import {
  Box,
  Card,
  CardMedia,
  CardContent,
  Typography,
  CircularProgress,
  Grid,
  IconButton,
} from '@mui/material';
import { Favorite as FavoriteIcon, FavoriteBorder as FavoriteBorderIcon } from '@mui/icons-material';
import { ImagePost } from '../types';

interface TimelineProps {
  images: ImagePost[];
  loading: boolean;
}

export default function Timeline({ images, loading }: TimelineProps) {
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (images.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h6" color="text.secondary">
          No images yet. Be the first to share!
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        Timeline
      </Typography>
      <Grid container spacing={3}>
        {images.map((image) => (
          <Grid item xs={12} key={image.id}>
            <Card
              sx={{
                transition: 'transform 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                },
              }}
            >
              <CardMedia
                component="img"
                image={image.image_url}
                alt={image.caption || 'Posted image'}
                sx={{
                  maxHeight: 600,
                  objectFit: 'contain',
                  backgroundColor: '#000',
                }}
              />
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box sx={{ flex: 1 }}>
                    {image.caption && (
                      <Typography variant="body1" sx={{ mb: 1 }}>
                        {image.caption}
                      </Typography>
                    )}
                    <Typography variant="caption" color="text.secondary">
                      {new Date(image.created_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                      })}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <IconButton
                      size="small"
                      sx={{
                        color: image.likes && image.likes > 0 ? 'error.main' : 'action.active',
                      }}
                    >
                      {image.likes && image.likes > 0 ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                    </IconButton>
                    {image.likes !== undefined && image.likes > 0 && (
                      <Typography variant="body2" color="text.secondary">
                        {image.likes}
                      </Typography>
                    )}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
