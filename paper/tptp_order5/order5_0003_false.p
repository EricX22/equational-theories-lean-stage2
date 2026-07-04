% order5_0003  eq1=57044 eq2=557  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,f(Y,Y)),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(Y,f(X,W)))) )).
