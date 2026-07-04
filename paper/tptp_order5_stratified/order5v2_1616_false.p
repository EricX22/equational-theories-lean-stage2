% order5v2_1616  eq1=2970 eq2=17729  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Y,Z)),W),Z) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(Y,Z),f(W,f(X,f(U,X)))) )).
