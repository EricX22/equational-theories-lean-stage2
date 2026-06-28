% hard3_0047  eq1=294 eq2=4155  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),Y),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(f(Y,X),X),Y) )).
