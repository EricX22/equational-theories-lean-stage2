% hard3_0363  eq1=3502 eq2=4109  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Z,Z),W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,X) != f(f(f(Y,Z),Z),Y) )).
