% hard3_0307  eq1=2874 eq2=2857  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Y)),X),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,f(X,Y)),Y),Z) )).
