%function[ rate_recov, rate_recov_byres ] = rot_anl( path, ftags, plotname )
close all;
clear all;
do_heatmaps = false;
%do_heatmaps = true;
path = '/Users/compbio/work/rotamers/protprot/perturbations/zdock4/';
ftags = { 'score12_corrdun02_dz'; 'score12opte_corrdun02_lksolv_1.6ion_dz'; 'score12resopte_corrdun02_lksolv_1.6ionequal_hbfree_dz'; };
plotname = 'pp.resopt_compare_dz';
cut_bfac = 1.0;
%path = '/Users/compbio/work/rotamers/yfset/nat/';
%ftags = { 'score12_corrdun02_dz'; 'score12opte_corrdun02_lksolv_1.6ion_dz'; 'score12resopte_corrdun02_lksolv_1.6ion_hbfree_dz'; };
%plotname = 'p.corrdun02_chip_edens';
%cut_bfac = 30.0;
%path = '/Users/compbio/work/dna/perturbations/new_interface_set/';
%ftags = { 'mydna_dun08_dz'; 'mydna_dun08_chisd1.4_dz'; 'mydna_dun08_chisd1.8_dz'; 'mydna_dun08_chisd2.2_dz'; 'mydna_dun08_chisd2.6_dz'; 'mydna_dun08_chisd3.0_dz' };
%plotname = 'dp.dun08onlymod_dz';
%{%}

ptags = { 'nat'; 'min'; 'rtmin' };
%filter cutoffs
cut_dscore = 0.001;
cut_farep = 5.0;
cut_rmsd = 0.8;
idx2aa = { 'A','C','D','E','F', 'G', 'H','I','K','L','M','N','P','Q','R','S','T','V','W','Y' };
naas = size( idx2aa, 2 );

%is this design or edensity data?
design = 0;
edens = 0;
%loadzen ze filez!!!
for i = 1:size( ftags, 1 ),
	matname = strcat( char( ftags( i ) ), '.anlmat' );
	matname = strcat( path, matname );
	if( exist( matname ) == 0 ), error( strcat( 'file  ', matname, ' not found!!' ) ); end
	mat_all = importdata( matname, '\t' );
	pdbsname = strcat( char( ftags( i ) ), '.anlpdb' );
	pdbsname = strcat( path, pdbsname );
	if( exist( pdbsname ) == 0 ), error( strcat( 'file  ', pdbsname, ' not found!!' ) ); end
	pdbs_all = importdata( pdbsname, '\t' );
	keyname = strcat( char( ftags( i ) ), '.anlkey' );
	keyname = strcat( path, keyname );
	if( exist( keyname ) == 0 ), error( strcat( 'file  ', keyname, ' not found!!' ) ); end
	key = importdata( keyname, '\t' );

	%check if all matrices same size
	if( i > 1 ),
		if( size( mat_all, 1 ) / numel( ptags ) ~= size( mat, 1 ) ), error( strcat( 'file  ', keyname, ' row mismatch!!' ) ); end
		if( size( mat_all, 2 ) ~= size( mat, 2 ) ), error( strcat( 'file  ', keyname, ' column mismatch!!' ) ); end
	end
	for ii = 1:size( ptags, 1 ),
		mat( :, :, ii ) = mat_all( mat_all( :, 1 ) == ii, :, : );
		pdbs( :, :, ii ) = pdbs_all( mat_all( :, 1 ) == ii, :, : ); 
	end
	clear mat_all pdbs_all;

	%findz ze keyz!!!
	ncol_tagidx = find( strcmp( key( : ), 'tagidx:' ), 1 );
	ncol_aaidx = find( strcmp( key( : ), 'aaidx:' ), 1 );
	ncol_faatr = find( strcmp( key( : ), 'fa_atr:' ), 1 );
	ncol_farep = find( strcmp( key( : ), 'fa_rep:' ), 1 );
	ncol_ref = find( strcmp( key( : ), 'fa_rep:' ), 1 );
	ncol_rmsd = find( ismember( key, 'scauto_rmsd_nat:' ), 1 );
	ncol_rmsd_min = find( ismember( key, 'scauto_rmsd_min:' ), 1 );
	ncol_score = find( ismember( key, 'total_score:' ), 1 );
	ncol_bfac = find( ismember( key, 'sc_bfactor:' ), 1 );
	ncol_schbonds = find( ismember( key, 'n_sc_hbonds:' ), 1 );
	ncol_fadunrot = find( ismember( key, 'fa_dun_rot:' ), 1 );
	ncol_fadundev = find( ismember( key, 'fa_dun_dev:' ), 1 );
	ncol_edens = find( ismember( key, 'elec_dens_window:' ), 1 );
	%was this an edens run? 
	if ncol_edens, edens = true; end

	%was this a design run? (cannot reset to zero)
	design = ( design || ( max( mat( :, ncol_aaidx, 3 ) ~= mat( :, ncol_aaidx, 1 ) ) > 0 ) );
	if design == 1, cut_bfac = 100; end

	%filterz ze rotamerz!!!
	fltr = ones( size( mat, 1 ), 1 ); 
	% bfactor < 1.0	
	fltr = fltr .* ( mat( :, ncol_bfac, 1 ) < cut_bfac ); 
	% no clash > 6.0 in nat
	fltr = fltr .* ( mat( :, ncol_farep, 1 ) < cut_farep ); 
	% no clash > 6.0 in min
	fltr = fltr .* ( mat( :, ncol_farep, 2 ) < cut_farep ); 
	% minimizer worked, we expect edens rt-into-density to be farther away
	if ~edens, fltr = fltr .* ( mat( :, ncol_score, 2 ) - mat( :, ncol_score, 1 ) < cut_dscore ); end
	% rtminimizer worked
	fltr = fltr .* ( mat( :, ncol_score, 3 ) - mat( :, ncol_score, 2 ) < cut_dscore ); 

	% get fltr mats for recov stats and score anls
	mat_fltr = mat( fltr == 1, :, : );
	nres_fltr = sum( repmat( mat_fltr( :, ncol_aaidx, 1 ), 1, naas ) == repmat( [1:naas], size( mat_fltr, 1 ), 1 ) );

	%which rtmined are better density? for those, replace native, fail based on edens score cutoff
	% ------- set nat = min for edens if min fits density better -----------
	if edens,
		edens_fltr = mat_fltr( :, ncol_edens, 2 ) <= mat_fltr( :, ncol_edens, 1 );
		mat( edens_fltr, :, 1 ) = mat( edens_fltr, :, 2 );
	end
	% -----------------------------------------------------------------------

	%%%%%%%%%%store rot/seqfail data%%%%%%%%%%%%%%

	%rotrecov? by rmsd
	if design == 0,
		fail = mat_fltr( :, ncol_rmsd, 3 ) > cut_rmsd;
	%or seqrecov? by aaidx
	else
		fail = mat_fltr( :, ncol_aaidx, 3 ) ~= mat_fltr( :, ncol_aaidx, 1 );
		%and get sequence transitions, normalized by seq counts
		seq_xsitions( :, :, i ) = hist3( mat_fltr( fail, ncol_aaidx, [1,3] ), [naas, naas] ) ./ repmat( nres_fltr', 1, naas );
%		seq_xsitions( :, :, i ) = hist3( mat_fltr( fail, ncol_aaidx, [1,3] ), [naas, naas] ); 
		%nres_fltr_dz = sum( repmat( mat_fltr( :, ncol_aaidx, 3 ), 1, naas ) == repmat( [1:naas], size( mat_fltr, 1 ), 1 ) );
	end
	mat_recov = mat_fltr( ~fail, :, : );

	%stats 
	rate_recov( i ) = size( mat_recov, 1 ) / size( mat_fltr, 1 );
	nres_recov = sum( repmat( mat_recov( :, ncol_aaidx, 1 ), 1, naas ) == repmat( [1:naas], size( mat_recov, 1 ), 1 ) );
	rate_recov_byres( i, : ) = nres_recov ./ nres_fltr;

	%%%%%%%%%%again for score diffs%%%%%%%%%%%%%%

	% fltr for scorecmp, things that dont move in minimization
	if edens, fltr_score = fltr;
	else, fltr_score = fltr .* ( mat( :, ncol_rmsd, 2 ) < cut_rmsd ); end

	mat_fltr_score = mat( fltr_score == 1, :, : );
	%must only subtract score, etc columns! ignores total score, make sure to use rtmin rmsd!
	scorecol_range = [ [ ncol_faatr:ncol_score-1 ], ncol_schbonds, ncol_fadunrot, ncol_fadundev ];
	mat_fltr_dscore = mat_fltr_score( :, :, 2 );
	mat_fltr_dscore( :, ncol_rmsd ) = mat_fltr_score( :, ncol_rmsd, 3 );
	mat_fltr_dscore( :, scorecol_range ) = mat_fltr_score( :, scorecol_range, 3 ) - mat_fltr_score( :, scorecol_range, 2 );
	
	nres_fltr_score = sum( repmat( mat_fltr_score( :, ncol_aaidx, 1 ), 1, naas ) == repmat( [1:naas], size( mat_fltr_score, 1 ), 1 ) );

	%rotrecov? by rmsd
	if design == 0,
		fail_score = mat_fltr_score( :, ncol_rmsd, 3 ) > cut_rmsd;
	%or seqrecov? by aaidx, set "rmsd" to 0 or 1
	else
		fail_score = mat_fltr_score( :, ncol_aaidx, 3 ) ~= mat_fltr_score( :, ncol_aaidx, 1 );
		mat_fltr_dscore( :, ncol_rmsd ) = fail_score;
	end
	mat_fail_score = mat_fltr_score( fail_score, :, : );
	mat_win_score = mat_fltr_score( ~fail_score, :, : );
	mat_fail_dscore = mat_fltr_dscore( fail_score, : ); 
	mat_win_dscore = mat_fltr_dscore( ~fail_score, : );


	%create mean/std dscore ( naas, n vals in mat line, ftag )
	%create corrcoef matrices ( naas, corr matrix dim1, corr matrix dim2, ftag )
	for i_aa = 1:naas,
		resfltr_fail = mat_fail_score( :, ncol_aaidx, 1 ) == i_aa;
		resfltr_win = mat_win_score( :, ncol_aaidx, 1 ) == i_aa;
		resfltr_fltr = mat_fltr_score( :, ncol_aaidx, 1 ) == i_aa;
		if sum( resfltr_fail ) > 1,
			mat_fail_dscore_mean( i_aa, :, i ) = mean( mat_fail_dscore( resfltr_fail, : ) );
			%line below will kill script if all res of type i_aa failed!!
			mat_win_dscore_mean( i_aa, :, i ) = mean( mat_win_dscore( resfltr_win, : ) );
			mat_fail_dscore_std( i_aa, :, i ) = std( mat_fail_dscore( resfltr_fail, : ) );
		else,
			mat_fail_dscore_mean( i_aa, :, i ) = zeros( 1, size( mat_fail_dscore, 2 ) );
			mat_win_dscore_mean( i_aa, :, i ) = mean( mat_win_dscore( resfltr_win, : ) );
			mat_fail_dscore_std( i_aa, :, i ) = zeros( 1, size( mat_fail_dscore, 2 ) );
		end

	        [ mat_dscore_corr, mat_dscore_pval ]  = corrcoef( mat_fltr_dscore( resfltr_fltr, : ) );
		if sum( resfltr_fltr ) > 1,
			this_cov = cov( mat_fltr_dscore( resfltr_fltr, : ) );
			mat_fltr_dscore_cov( i_aa, :, i ) = this_cov( ncol_rmsd, : );
			rmsd_dscore_corr( i_aa, :, i ) =  mat_dscore_corr( :, ncol_rmsd );
	      		rmsd_dscore_pval( i_aa, :, i ) =  mat_dscore_pval( :, ncol_rmsd );
		else,
			mat_fltr_dscore_cov( i_aa, :, i ) = zeros( 1, size( mat_fltr_dscore, 2 ) );
			rmsd_dscore_corr( i_aa, :, i ) =  zeros( 1, size( mat_fltr_dscore, 2 ) );
	      		rmsd_dscore_pval( i_aa, :, i ) =  ones( 1, size( mat_fltr_dscore, 2 ) );
		end
	end
end

%de-NaNify
rate_recov_byres( find( isnan( rate_recov_byres ) ) ) = zeros( size( find( isnan( rate_recov_byres ) ) ) );
mat_fail_dscore_mean( find( isnan( mat_fail_dscore_mean ) ) ) = zeros( size( find( isnan( mat_fail_dscore_mean ) ) ) );
mat_win_dscore_mean( find( isnan( mat_win_dscore_mean ) ) ) = zeros( size( find( isnan( mat_win_dscore_mean ) ) ) );
mat_fail_dscore_std( find( isnan( mat_fail_dscore_std ) ) ) = zeros( size( find( isnan( mat_fail_dscore_std ) ) ) );
rmsd_dscore_corr( find( isnan( rmsd_dscore_corr ) ) ) = zeros( size( find( isnan( rmsd_dscore_corr ) ) ) );
rmsd_dscore_pval( find( isnan( rmsd_dscore_pval ) ) ) = zeros( size( find( isnan( rmsd_dscore_pval ) ) ) );
seq_xsitions( find( isnan( seq_xsitions ) ) ) = zeros( size( find( isnan( seq_xsitions ) ) ) );

%calc seq entropy normalized rate recov
rate_recov_norm = mean( rate_recov_byres, 2 );

%replace _'s in output text, add recov rate to tagname
ftags_out = strrep( ftags, '_', '-' );
for itags = 1:numel( ftags_out ),
	ftags_legend{ itags } = strcat( ftags_out{ itags }, '::', num2str( rate_recov( itags ), 2 ), '::', num2str( rate_recov_norm( itags ), 2 ) );
end

%rotrecov plot
figure(); hold on;
bar( rate_recov_byres' )
%plot( nres_fltr ./ sum( nres_fltr ), 'k^', 'MarkerFaceColor', 'w', 'MarkerSize', 8 );
%if design == 1, plot( nres_fltr_dz ./ sum( nres_fltr_dz ), 'k^', 'MarkerFaceColor', 'm', 'MarkerSize', 8 ); end
set( gca,'XTick',1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
xlabel( int2str( sum( nres_fltr ) ) );
ylim_recov = min( min( rate_recov_byres( :, sum( rate_recov_byres ) > 0 ) ) );
set( gca,'YLim', [ylim_recov 1.0] );
legend( ftags_legend , 'Location', 'SouthOutside', 'FontSize', 8 );

plotname_this = strcat( 'rotrecov.', plotname );
if design == 1, plotname_this = strcat( 'seqrecov.', plotname ); end
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

%{
%percent of aa in total set
figure(); hold on;
bar( nres_fltr ./ sum( nres_fltr ), 'FaceColor', 'k' )
set( gca,'XTick',1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
xlabel( int2str( sum( nres_fltr ) ) );
plotname_this = strcat( 'aatot.', plotname );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;
%}

%???	generate heatmaps	???
if do_heatmaps,

%delta scores
%slice out score terms only
mat_fail_dscore_mean = mat_fail_dscore_mean( :, scorecol_range, : );
mat_win_dscore_mean = mat_win_dscore_mean( :, scorecol_range, : );
mat_fail_dscore_std = mat_fail_dscore_std( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
mat_fail_dscore_std_red = mat_fail_dscore_std( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
mat_fail_dscore_mean_red = mat_fail_dscore_mean( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
mat_win_dscore_mean_red = mat_win_dscore_mean( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
mat_failminuswin_dscore_mean_red = mat_fail_dscore_mean_red - mat_win_dscore_mean_red;

%slice out score terms only
mat_fltr_dscore_cov = mat_fltr_dscore_cov( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
mat_fltr_dscore_cov_red = mat_fltr_dscore_cov( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );

%slice out score terms only
rmsd_dscore_corr = rmsd_dscore_corr( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
rmsd_dscore_corr_red = rmsd_dscore_corr( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );

for i = 1:size( ftags, 1 ),

figure(); 
imagesc( rot90( mat_failminuswin_dscore_mean_red( :, :, i ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
min_tot = min( min( min( mat_failminuswin_dscore_mean_red( :, :, : ) ) ) );
max_tot = max( max( max( mat_failminuswin_dscore_mean_red( :, :, : ) ) ) );
caxis( [ min_tot, max_tot ] );
colorbar;
colormap( 'spring' );
plotname_this = strcat( 'dnrg.', plotname, '.', ftags_out{ i } );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

%delta scores covariance w/ rmsd
%only do if rmsd is meaningful!


figure(); 
imagesc( rot90( mat_fltr_dscore_cov_red( :, :, i ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
min_tot = min( min( min( mat_fltr_dscore_cov_red( :, :, : ) ) ) );
max_tot = max( max( max( mat_fltr_dscore_cov_red( :, :, : ) ) ) );
caxis( [ min_tot, max_tot ] );
colorbar;
colormap( 'winter' );
plotname_this = strcat( 'rmscov.', plotname, '.', ftags_out{ i } );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

figure(); 
imagesc( rot90( rmsd_dscore_corr_red( :, :, i ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
min_tot = min( min( min( mat_fltr_dscore_cov_red( :, :, : ) ) ) );
max_tot = max( max( max( mat_fltr_dscore_cov_red( :, :, : ) ) ) );
caxis( [ min_tot, max_tot ] );
colorbar;
colormap( 'cool' );
plotname_this = strcat( 'rmscorr.', plotname, '.', ftags_out{ i } );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

if design == 1,
	figure(); 
	imagesc( rot90( seq_xsitions( :, :, i ) ) )
	set( gca,'XTick', 1:numel( idx2aa ) );
	set( gca,'XTickLabel', idx2aa );
	set( gca,'YTick', 1:numel( idx2aa ) );
	set( gca,'YTickLabel', rot90( idx2aa, 2 ) );
	xlabel( 'FROM' );
	ylabel( 'OT' );
	min_tot = 0;
	max_tot = max( max( max( seq_xsitions( :, :, : ) ) ) );
	caxis( [ min_tot, max_tot ] );
	colorbar;
	colormap( 'hot' );
	plotname_this = strcat( 'xsitions.', plotname, '.', ftags_out{ i } );
	title( plotname_this );
	saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
	hold off;
end

end

end

%{

%delta scores
%slice out score terms only
mat_fail_dscore_mean = mat_fail_dscore_mean( :, scorecol_range, : );
mat_fail_dscore_std = mat_fail_dscore_std( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
mat_fail_dscore_std_red = mat_fail_dscore_std( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
mat_fail_dscore_mean_red = mat_fail_dscore_mean( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
figure(); 
%only plotting ftag 1 rght now
imagesc( rot90( mat_fail_dscore_mean_red( :, :, 1 ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
absmax_dscore = max( abs( min( min( mat_fail_dscore_mean_red( :, :, 1 ) ) ) ), abs( max( max( mat_fail_dscore_mean_red( :, :, 1 ) ) ) ) );
%caxis( [ -absmax_dscore, absmax_dscore ] );
colorbar;
colormap( 'spring' );

plotname_this = strcat( 'dnrg.', plotname );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

%delta scores covariance w/ rmsd
%only do if rmsd is meaningful!
if design == 0,

%slice out score terms only
mat_fltr_dscore_cov = mat_fltr_dscore_cov( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
mat_fltr_dscore_cov_red = mat_fltr_dscore_cov( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
figure(); 
%only plotting ftag 1 rght now
imagesc( rot90( mat_fltr_dscore_cov_red( :, :, 1 ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
absmax_dscore = max( abs( min( min( mat_fltr_dscore_cov_red( :, :, 1 ) ) ) ), abs( max( max( mat_fltr_dscore_cov_red( :, :, 1 ) ) ) ) );
caxis( [ -absmax_dscore, absmax_dscore ] );
colorbar;
colormap( 'winter' );

plotname_this = strcat( 'rmscov.', plotname );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;

%slice out score terms only
rmsd_dscore_corr = rmsd_dscore_corr( :, scorecol_range, : );
key_scorecol = key( scorecol_range )';
key_scorecol_red = key_scorecol( max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0 );
rmsd_dscore_corr_red = rmsd_dscore_corr( :, max( max( abs( mat_fail_dscore_mean ) ), [], 3 ) > 0, : );
figure(); 
%only plotting ftag 1 rght now
imagesc( rot90( rmsd_dscore_corr_red( :, :, 1 ) ) )
set( gca,'XTick', 1:numel( idx2aa ) );
set( gca,'XTickLabel', idx2aa );
set( gca,'YTick', 1:numel( key_scorecol_red ) );
set( gca,'YTickLabel', rot90( key_scorecol_red, 2 ) );
xlabel( int2str( sum( nres_fltr ) ) );
absmax_dscore = max( abs( min( min( rmsd_dscore_corr_red( :, :, 1 ) ) ) ), abs( max( max( rmsd_dscore_corr_red( :, :, 1 ) ) ) ) );
%caxis( [ -absmax_dscore, absmax_dscore ] );
colorbar;
colormap( 'hot' );

plotname_this = strcat( 'rmscorr.', plotname );
title( plotname_this );
saveas( gcf, strcat( path, plotname_this, '.png' ), 'png' );
hold off;


end

%}
