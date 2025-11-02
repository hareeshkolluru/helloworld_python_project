import { useState } from 'react';
import {
  Card,
  CardContent,
  Button,
  Box,
  Typography,
  LinearProgress,
  Alert,
  TextField,
} from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';

interface ImageUploadProps {
  onImageUploaded: () => void;
}

export default function ImageUpload({ onImageUploaded }: ImageUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [caption, setCaption] = useState('');
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        return;
      }
      setSelectedFile(file);
      setError(null);
      setSuccess(false);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('caption', caption);

    try {
      const response = await fetch('/api/v1/images', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      setSuccess(true);
      setSelectedFile(null);
      setCaption('');
      setPreview(null);
      onImageUploaded();
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError('Failed to upload image. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setCaption('');
    setPreview(null);
    setError(null);
    setSuccess(false);
  };

  return (
    <Card sx={{ mb: 4 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Share a moment
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Image uploaded successfully!
          </Alert>
        )}

        {preview && (
          <Box
            sx={{
              mb: 2,
              borderRadius: 2,
              overflow: 'hidden',
              maxHeight: 400,
              display: 'flex',
              justifyContent: 'center',
              backgroundColor: '#000',
            }}
          >
            <img
              src={preview}
              alt="Preview"
              style={{
                maxWidth: '100%',
                maxHeight: '400px',
                objectFit: 'contain',
              }}
            />
          </Box>
        )}

        <TextField
          fullWidth
          placeholder="Add a caption..."
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          sx={{ mb: 2 }}
          disabled={uploading}
        />

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Button
            component="label"
            variant="outlined"
            startIcon={<CloudUploadIcon />}
            disabled={uploading}
          >
            Choose Image
            <input
              type="file"
              hidden
              accept="image/*"
              onChange={handleFileSelect}
            />
          </Button>

          {selectedFile && (
            <>
              <Button
                variant="contained"
                onClick={handleUpload}
                disabled={uploading}
                sx={{ minWidth: 100 }}
              >
                {uploading ? 'Uploading...' : 'Post'}
              </Button>
              <Button
                variant="text"
                onClick={handleClear}
                disabled={uploading}
              >
                Clear
              </Button>
            </>
          )}
        </Box>

        {uploading && <LinearProgress sx={{ mt: 2 }} />}
      </CardContent>
    </Card>
  );
}
