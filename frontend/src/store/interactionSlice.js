import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  formData: {
    hcp_name: '',
    interaction_date: new Date().toISOString().split('T')[0],
    sentiment: '',
    products_discussed: '',
    materials_shared: [],
    interaction_type: '',
    location: '',
    duration_minutes: '',
    notes: '',
    follow_up_date: '',
    follow_up_action: '',
  },
  currentInteractionId: null,
  chatMessages: [],
  isLoading: false,
  error: null,
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateFormField: (state, action) => {
      const { field, value } = action.payload;
      state.formData[field] = value;
    },
    updateMultipleFields: (state, action) => {
      state.formData = { ...state.formData, ...action.payload };
    },
    resetForm: (state) => {
      state.formData = initialState.formData;
      state.currentInteractionId = null;
    },
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    setCurrentInteractionId: (state, action) => {
      state.currentInteractionId = action.payload;
    },
  },
});

export const {
  updateFormField,
  updateMultipleFields,
  resetForm,
  addChatMessage,
  setLoading,
  setError,
  setCurrentInteractionId,
} = interactionSlice.actions;

export default interactionSlice.reducer;

