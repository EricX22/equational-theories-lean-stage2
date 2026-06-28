% hard3_0036  eq1=204 eq2=1426  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(X,X)),Y) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(f(X,X),f(X,f(X,X))) )).
