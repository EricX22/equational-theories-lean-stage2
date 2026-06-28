% hard3_0317  eq1=2927 eq2=4611  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,X),Y) != f(f(Y,Z),Y) )).
