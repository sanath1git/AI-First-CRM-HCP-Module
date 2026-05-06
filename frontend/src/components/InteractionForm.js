import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateFormField, resetForm } from '../store/interactionSlice';
import { interactionAPI } from '../services/api';
import './InteractionForm.css';

const InteractionForm = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.interaction.formData);
  const currentInteractionId = useSelector((state) => state.interaction.currentInteractionId);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateFormField({ field: name, value }));
  };

  const handleCheckboxChange = (material) => {
    const currentMaterials = formData.materials_shared || [];
    let updatedMaterials;

    if (currentMaterials.includes(material)) {
      updatedMaterials = currentMaterials.filter(m => m !== material);
    } else {
      updatedMaterials = [...currentMaterials, material];
    }

    dispatch(updateFormField({ field: 'materials_shared', value: updatedMaterials }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (currentInteractionId) {
        await interactionAPI.update(currentInteractionId, formData);
        alert('Interaction updated successfully!');
      } else {
        const result = await interactionAPI.create(formData);
        alert('Interaction created successfully!');
        console.log('Created:', result);
      }
    } catch (error) {
      console.error('Error saving interaction:', error);
      alert('Error saving interaction. Please try again.');
    }
  };

  const handleReset = () => {
    dispatch(resetForm());
  };

  return (
    <div className="interaction-form">
      <h2>HCP Interaction Details</h2>

      <div className="info-banner">
        Use the AI Assistant on the right to fill this form automatically!
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="hcp_name">HCP Name *</label>
          <input
            type="text"
            id="hcp_name"
            name="hcp_name"
            value={formData.hcp_name}
            onChange={handleInputChange}
            placeholder="e.g., Dr. Smith"
            required
          />
        </div>

        <div className="form-group-row">
          <div className="form-group">
            <label htmlFor="interaction_date">Interaction Date *</label>
            <input
              type="date"
              id="interaction_date"
              name="interaction_date"
              value={formData.interaction_date}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="sentiment">Sentiment</label>
            <select
              id="sentiment"
              name="sentiment"
              value={formData.sentiment}
              onChange={handleInputChange}
            >
              <option value="">Select sentiment</option>
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
            </select>
          </div>
        </div>

        <div className="form-group-row">
          <div className="form-group">
            <label htmlFor="interaction_type">Interaction Type</label>
            <select
              id="interaction_type"
              name="interaction_type"
              value={formData.interaction_type}
              onChange={handleInputChange}
            >
              <option value="">Select type</option>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
              <option value="Conference">Conference</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="duration_minutes">Duration (minutes)</label>
            <input
              type="number"
              id="duration_minutes"
              name="duration_minutes"
              value={formData.duration_minutes}
              onChange={handleInputChange}
              placeholder="e.g., 30"
              min="0"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="location">Location</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="e.g., Hospital XYZ"
          />
        </div>

        <div className="form-group">
          <label htmlFor="products_discussed">Products Discussed</label>
          <input
            type="text"
            id="products_discussed"
            name="products_discussed"
            value={formData.products_discussed}
            onChange={handleInputChange}
            placeholder="e.g., Product X, Product Y"
          />
        </div>

        <div className="form-group">
          <label>Materials Shared</label>
          <div className="checkbox-group">
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="brochure"
                checked={formData.materials_shared?.includes('brochure')}
                onChange={() => handleCheckboxChange('brochure')}
              />
              <label htmlFor="brochure">Brochure</label>
            </div>
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="sample"
                checked={formData.materials_shared?.includes('sample')}
                onChange={() => handleCheckboxChange('sample')}
              />
              <label htmlFor="sample">Sample</label>
            </div>
            <div className="checkbox-item">
              <input
                type="checkbox"
                id="presentation"
                checked={formData.materials_shared?.includes('presentation')}
                onChange={() => handleCheckboxChange('presentation')}
              />
              <label htmlFor="presentation">Presentation</label>
            </div>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleInputChange}
            placeholder="Additional details about the interaction..."
          />
        </div>

        <div className="form-group-row">
          <div className="form-group">
            <label htmlFor="follow_up_date">Follow-up Date</label>
            <input
              type="date"
              id="follow_up_date"
              name="follow_up_date"
              value={formData.follow_up_date}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="follow_up_action">Follow-up Action</label>
            <input
              type="text"
              id="follow_up_action"
              name="follow_up_action"
              value={formData.follow_up_action}
              onChange={handleInputChange}
              placeholder="e.g., Schedule demo"
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {currentInteractionId ? 'Update Interaction' : 'Save Interaction'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={handleReset}>
            Clear Form
          </button>
        </div>
      </form>
    </div>
  );
};

export default InteractionForm;

