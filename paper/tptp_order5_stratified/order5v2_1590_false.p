% order5v2_1590  eq1=37073 eq2=14981  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),f(Z,W)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(Z,Y),f(W,Y)),Y)) )).
