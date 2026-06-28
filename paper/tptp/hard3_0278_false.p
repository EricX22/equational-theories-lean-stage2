% hard3_0278  eq1=2661 eq2=331  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,Y),f(X,X)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(Z,W)) )).
