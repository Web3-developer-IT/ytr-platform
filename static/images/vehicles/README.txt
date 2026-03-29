Yours To Rent — vehicle imagery
================================

- Listing photos uploaded through /listing/add/ are stored on Cloudinary under the
  folder path "vehicles/listings/..." (see core.models.ListingImage).

- For static marketing assets (decks, PDFs, investor pages), add high-resolution
  vehicle shots into this directory and reference them with:
    {% static 'images/vehicles/your-file.jpg' %}

- Default card fallback (browse/home) when a listing has no photo is set in
  settings YTR_DEFAULT_VEHICLE_IMAGE_URL (override via environment variable).
