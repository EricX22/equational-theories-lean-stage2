% order5v2_0668  eq1=14959 eq2=47513  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),f(Z,X)),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,Z),f(f(W,Z),Z)) )).
