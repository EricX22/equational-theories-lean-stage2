% hard3_0336  eq1=3171 eq2=99  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),W),X) )).
fof(neg, negated_conjecture, ? [X] : ( X != f(X,f(f(X,X),X)) )).
