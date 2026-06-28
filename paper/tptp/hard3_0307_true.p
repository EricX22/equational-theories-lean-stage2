% hard3_0307  eq1=2874 eq2=2857  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Y)),X),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(X,Y)),Y),Z) )).
