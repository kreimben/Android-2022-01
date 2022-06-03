package com.example.ch10

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.navigation.findNavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.*
import com.example.ch10.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var appBarConf: AppBarConfiguration

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val navHostingFragment =
            supportFragmentManager.findFragmentById(R.id.fragment) as NavHostFragment
        val navController = navHostingFragment.navController
        val topDest = setOf(R.id.homeFragment, R.id.page1Fragment, R.id.page2Fragment, R.id.myDialogFragment)

        appBarConf = AppBarConfiguration(topDest, binding.drawerLayout)
        setupActionBarWithNavController(navController, appBarConf)
        binding.navView.setupWithNavController(navController)
    }

    override fun onSupportNavigateUp(): Boolean {
        return findNavController(R.id.fragment).navigateUp(appBarConf) || super.onSupportNavigateUp()
    }
}