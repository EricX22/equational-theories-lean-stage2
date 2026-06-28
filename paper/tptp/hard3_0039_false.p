% hard3_0039  eq1=209 eq2=1430  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(X,f(Y,X)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,X),f(X,f(Y,Z))) )).
