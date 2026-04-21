<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;


class LoginController extends Controller
{
     public function showLoginForm()
    {
        // Jika user sudah login, redirect ke dashboard
        if (session()->has('id_user') && session()->has('role')) {
            return redirect()->route('dashboard');
        }

        return view('login');
    }

    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required|min:20',
        ]);

        try {
            $response = Http::post('http://localhost:8080/api/auth/login', [
                'email' => $request->email,
                'password' => $request->password,
            ]);

            if ($response->successful()) {
                $data = $response->json();

                // Cek apakah respons memiliki data user dan role
                if (!isset($data['user'])) {
                    return back()->withErrors([
                        'login_error' => 'Data user atau role tidak ditemukan dari API.'
                    ])->withInput($request->only('email'));
                }

                $user = $data['user'];

                if (!isset($user['email']) || !isset($user['role'])) {
                    return back()->withErrors([
                        'login_error' => 'Data user atau role tidak lengkap dari API.'
                    ])->withInput($request->only('email'));
                }

                // Validasi role harus admin atau instansi
                if (!in_array($user['role'], ['admin', 'instansi'])) {
                    return back()->withErrors([
                        'login_error' => 'Role tidak valid.'
                    ])->withInput($request->only('email'));
                }

                session()->flush();
                // Simpan data ke session, termasuk user dan role
                session([
                    'id_user' => $user['id_user'],
                    'email' => $user['email'],
                    'nama' => $user['nama'] ?? $user['nama'] ?? 'Admin',
                    'role' => $user['role'],
                    'user' => (object) $user,
                    'logged_in' => true
                ]);
                $request->session()->regenerate();

                return redirect()->route('dashboard')->with('success', 'Login berhasil!');
            }

            // Tampilkan pesan error dari API jika ada
            return back()->withErrors([
                'login_error' => $response->json()['message'] ?? 'Login gagal'
            ]);

        } catch (\Exception $e) {
            return back()->withErrors([
                'login_error' => 'Server error: ' . $e->getMessage()
            ]);
        }
    }

    public function logout()
    {
        // Hapus semua session
        session()->flush();
        return redirect()->route('login')->with('success', 'Logout berhasil!');
    }
}
