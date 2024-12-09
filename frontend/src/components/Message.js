import { h } from 'preact';

const Message = ({ text, sender }) => (
  <div class={`message ${sender === 'user' ? 'user' : 'other'}`}>
    {text}
  </div>
);

export default Message;