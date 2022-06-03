package com.example.ch12

import android.content.Intent
import android.graphics.Typeface
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.Settings
import android.util.TypedValue
import android.widget.TextView
import androidx.preference.PreferenceManager
import com.example.ch12.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val binding = ActivityMainBinding.inflate(layoutInflater)
        val tv = binding.textView

        setContentView(binding.root)

        tv.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
    }

    override fun onStart() {
        super.onStart()

        val tv = findViewById<TextView>(R.id.textView)

        // Small 10sp
        // Medium 14sp
        // Big 20sp
        val pm = PreferenceManager.getDefaultSharedPreferences(this)
        val saved_name = pm.getString("name", "Hello, World!")
        val saved_size = pm.getString("size", "10.0f")!!.toFloat()
        val is_italic = pm.getBoolean("italic", false)

//        Snackbar.make(this, tv, "${saved_name}", Snackbar.LENGTH_SHORT).show()

        tv.text = saved_name
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, saved_size)
        if (is_italic) tv.setTypeface(null, Typeface.ITALIC)
    }
}