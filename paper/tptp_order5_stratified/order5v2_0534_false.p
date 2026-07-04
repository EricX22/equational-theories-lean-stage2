% order5v2_0534  eq1=13849 eq2=7647  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(f(X,Z),Z)),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(X,f(f(Z,f(Z,Z)),Z))) )).
