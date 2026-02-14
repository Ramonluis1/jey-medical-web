
// Supabase Configuration
// In a production environment, variables should be secured.
const SUPABASE_URL = 'https://kjocjhmwtsalfrxiqpnr.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtqb2NqaG13dHNhbGZyeGlxcG5yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA1OTUwNzUsImV4cCI6MjA4NjE3MTA3NX0.b-ZheXXLezVd7FxtOnPzC-bPXHR2nPDD3c9VHNbw-e0';

// Initialize Supabase Client
// Ensure the Supabase JS library is loaded before this script runs
// <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Auth Helper Functions
async function signUp(email, password) {
    const { data, error } = await supabase.auth.signUp({
        email: email,
        password: password,
    });
    return { data, error };
}

async function signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password,
    });
    return { data, error };
}

async function signOut() {
    const { error } = await supabase.auth.signOut();
    return { error };
}

async function getCurrentUser() {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
}

async function resetPasswordForEmail(email) {
    // This sends a password reset email to the user.
    // The user will receive a link to click, which will log them in.

    const options = {};

    // Supabase requires a valid HTTP/HTTPS URL for redirection.
    // 'file://' protocol is NOT supported by the API and will cause an error (400).
    // If running from a local file, we omit 'redirectTo' to let Supabase use the default Site URL defined in the dashboard.
    if (window.location.protocol.startsWith('http')) {
        options.redirectTo = window.location.href;
    }

    const { data, error } = await supabase.auth.resetPasswordForEmail(email, options);
    return { data, error };
}

// Expose functions to global scope for HTML access
window.signUp = signUp;
window.signIn = signIn;
window.signOut = signOut;
window.getCurrentUser = getCurrentUser;
window.resetPasswordForEmail = resetPasswordForEmail;
window.logHistory = logHistory;
window.getUserHistory = getUserHistory;

// History Helper Functions
async function logHistory(activityType, details = {}) {
    const user = await getCurrentUser();
    if (!user) return; // Only log for logged-in users

    const { error } = await supabase
        .from('user_history')
        .insert([
            {
                user_id: user.id,
                activity_type: activityType,
                details: details
            }
        ]);

    if (error) console.error('Error logging history:', error);
}

async function getUserHistory() {
    const user = await getCurrentUser();
    if (!user) return { data: [], error: 'No user' };

    const { data, error } = await supabase
        .from('user_history')
        .select('*')
        .order('created_at', { ascending: false });

    return { data, error };
}
